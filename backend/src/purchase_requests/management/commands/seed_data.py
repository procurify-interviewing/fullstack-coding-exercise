"""
Seed a small, deterministic dataset.

  python manage.py seed_data

Users (username -> id after a fresh migrate):
  alice -> 1   creates most requests
  bob   -> 2   approver on many requests, creates none
  carol -> 3   both requests and approves

Notes for whoever runs this:
  - Users are reused rather than recreated, so their ids stay stable across re-runs.
  - created_at is assigned in groups, so several requests share the exact same timestamp.
  - A handful of requests are soft-deleted (soft_deleted set).
"""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from purchase_requests.models import Approval, PurchaseRequest

User = get_user_model()

TITLES = [
    "Laptops for new hires",
    "Office chairs",
    "Conference sponsorship",
    "SaaS renewal",
    "Catering for offsite",
    "Warehouse shelving",
    "Marketing print run",
    "Lab consumables",
]


class Command(BaseCommand):
    help = "Reset and seed users, purchase requests and approvals for the exercise."

    @transaction.atomic
    def handle(self, *args, **options):
        Approval.objects.all().delete()
        PurchaseRequest.objects.all().delete()

        alice, bob, carol = (self._get_or_create_user(name) for name in ("alice", "bob", "carol"))

        requesters = [alice, alice, carol, alice, carol]
        statuses = [
            PurchaseRequest.Status.PENDING,
            PurchaseRequest.Status.PENDING,
            PurchaseRequest.Status.APPROVED,
            PurchaseRequest.Status.DRAFT,
            PurchaseRequest.Status.REJECTED,
            PurchaseRequest.Status.PENDING,
        ]
        base = timezone.now().replace(microsecond=0) - timedelta(days=30)

        prs = []
        for i in range(60):
            prs.append(
                PurchaseRequest(
                    requester=requesters[i % len(requesters)],
                    title=f"{TITLES[i % len(TITLES)]} #{i + 1}",
                    status=statuses[i % len(statuses)],
                    total_amount=Decimal("125.00") * (i % 13 + 1),
                    # Groups of 4 share the same created_at on purpose.
                    created_at=base + timedelta(hours=i // 4),
                    soft_deleted=(i % 11 == 10),
                )
            )
        PurchaseRequest.objects.bulk_create(prs)
        prs = list(PurchaseRequest.objects.order_by("id"))

        approvals = []
        # Counted over pending requests rather than over `prs`, so the cadence below does not
        # line up with the repeating `statuses` cycle.
        pending_seen = 0
        for pr in prs:
            if pr.status == PurchaseRequest.Status.DRAFT:
                continue
            decided = pr.created_at + timedelta(hours=2)
            if pr.status == PurchaseRequest.Status.PENDING:
                # Bob still has to decide. Every second pending PR also has Carol, who has
                # signed off on half of those and still owes a decision on the rest.
                approvals.append(Approval(purchase_request=pr, approver=bob, approved=None))
                if pending_seen % 2 == 0 and pr.requester_id != carol.id:
                    carol_approved = True if pending_seen % 4 == 0 else None
                    approvals.append(
                        Approval(
                            purchase_request=pr,
                            approver=carol,
                            approved=carol_approved,
                            decided_at=decided if carol_approved is not None else None,
                        )
                    )
                pending_seen += 1
            elif pr.status == PurchaseRequest.Status.APPROVED:
                approvals.append(Approval(purchase_request=pr, approver=bob, approved=True, decided_at=decided))
            elif pr.status == PurchaseRequest.Status.REJECTED:
                approver = carol if pr.requester_id != carol.id else bob
                approvals.append(
                    Approval(purchase_request=pr, approver=approver, approved=False, decided_at=decided)
                )
        Approval.objects.bulk_create(approvals)

        self.stdout.write(
            self.style.SUCCESS(
                f"Seeded {User.objects.count()} users, {PurchaseRequest.objects.count()} purchase requests "
                f"({PurchaseRequest.objects.filter(soft_deleted=True).count()} soft-deleted), "
                f"{Approval.objects.count()} approvals."
            )
        )
        for u in (alice, bob, carol):
            self.stdout.write(f"  {u.username}: id={u.id}")

    @staticmethod
    def _get_or_create_user(username: str):
        user, _ = User.objects.get_or_create(
            username=username, defaults={"email": f"{username}@example.com"}
        )
        return user

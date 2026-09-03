# Stage 1: List Purchase Requests

Implement `GET /api/purchase-requests/`.

The endpoint returns the purchase requests the current user is allowed to see:

- requests they created, or
- requests where they are an approver.

Filters (query string):

- `status=<STATUS>`
- `requires_my_approval=true` - only requests where the current user still has a pending approval

Each item in the response:

- `id`, `status`, `total_amount`, `requester_id`, `created_at`
- `requires_my_approval` - computed for the current user

Models are in `purchase_requests/models.py`. Sample data: `python manage.py seed_data`.

Anything not specified here is a decision for you to make or a question for you to ask.

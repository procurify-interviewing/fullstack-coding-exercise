# Backend: Purchase Requests API

Build an approver-aware Purchase Requests API that serves purchase requests over HTTP.

- Models are predefined in `src/purchase_requests/models.py` (`PurchaseRequest`,
  `Approval`). If you want to change them, say so first.
- Sample data is already seeded by `make setup` (or `python manage.py seed_data`): 60
  purchase requests and the users `alice` (id 1), `bob` (id 2) and `carol` (id 3). Some
  requests are flagged `soft_deleted`.
- The stub is `src/purchase_requests/views.py`; it currently answers `501 Not Implemented`.
- Django REST Framework is installed and configured. Using it is optional.
- Anything not specified here is a decision for you to make or a question to ask. Be ready
  to talk through the calls you made, and write it as if it were going to production.

## Authentication

There is no auth layer in this project - `DEFAULT_AUTHENTICATION_CLASSES` is empty in
`config/settings.py`. Mock the current user however you like, and say which approach you
chose and why.

Both the visibility rule and `requires_my_approval` are computed relative to that user.
Pick one of the seeded users so there is data to see - `bob` (id 2) approves a lot and
creates nothing, which makes for a good default.

## Part 1: List purchase requests

`GET /api/purchase-requests/` returns the purchase requests the current user is allowed to
see:

- requests they created, or
- requests where they are an approver.

Each item carries `requires_my_approval`, computed for the current user: true when that
user has an `Approval` row on the request whose `approved` is still null.

### Query parameters

| Param | Values | Description |
| --- | --- | --- |
| `status` | `DRAFT`, `PENDING`, `APPROVED`, `REJECTED` | Filter by status. Omit for all. |
| `requires_my_approval` | `true` | Only requests still awaiting the current user's decision. |

### Response

`GET /api/purchase-requests/?status=PENDING&requires_my_approval=true`

```json
{
  "data": [
    {
      "id": 7,
      "requester_name": "alice",
      "status": "PENDING",
      "total_amount": "1000.00",
      "requires_my_approval": true
    }
  ]
}
```

### Show it working

Any one of these is fine:

- `make run-backend`, then open
  <http://localhost:8000/api/purchase-requests/?status=PENDING&requires_my_approval=true>
  in a browser.
- Hit the same URL with `curl`, or a free HTTP client - Hoppscotch, Bruno, Postman, or the
  VS Code REST Client extension.
- Flesh out `src/tests/test_purchase_request_api.py` and run `make test-backend`. Fixtures
  live in `src/tests/conftest.py`, helpers in `src/tests/factories.py`.

Walk through at least: an unfiltered result, a filtered result, and a request the current
user can see but does not have to approve.

## Part 2: Add pagination

The same endpoint accepts `limit` and `offset` and returns a `pagination` block alongside
`data`. The Part 1 filters keep working, and are applied before the slice.

`count` is the total number of matching rows, not the size of the current page - the
frontend's "Load More" button needs it to know when to stop.

Decide and state:

- a default `limit` and a maximum `limit`,
- a stable ordering (the seed data gives groups of requests identical `created_at` values
  on purpose, so `created_at` alone is not a stable sort key),
- what happens for invalid or out-of-range values.

### Query parameters

| Param | Values | Description |
| --- | --- | --- |
| `limit` | integer | Page size. Pick a default and a cap. |
| `offset` | integer | Rows to skip. Defaults to `0`. |
| `status`, `requires_my_approval` | | As in Part 1. |

### Response

`GET /api/purchase-requests/?limit=20&offset=20`

```json
{
  "data": [
    {
      "id": 27,
      "requester_name": "carol",
      "status": "PENDING",
      "total_amount": "375.00",
      "requires_my_approval": false
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 20,
    "count": 54
  }
}
```

### Show it working

Same three routes as Part 1. Walk a couple of pages - `?limit=5&offset=0`, then
`?limit=5&offset=5` - and show that the ids neither repeat nor skip, that `count` stays
constant across pages, and that it shrinks when a `status` filter is applied.

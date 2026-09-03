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

# Stage 2: View and approve purchase requests

Build a REACT component that shows purchase requests requiring my approval, and allows me to approve them.

## Part 1: fetch and render a list of purchase requests

- Call this endpoint: `GET: /api/purchase-requests`, it is mocked to return a list response
  - use react hooks to fetch the list of purchase requests and store them in `<App />` state on component mount
- Pass the list of PRs returned by the GET request to `<ListRequests />`
  - define component props
  - render a table with a static header row and dynamic content rows
    - Amount
    - Requester ID
    - Status

## Part 2: approve pending purchase requests

- Add a column to `ListRequests.tsx` that renders an `<ApproveRequest />` in each row
- Define a `handleApproveRequest()` function in App.tsx that is passed down to `ApproveRequest.tsx` through `ListRequests.tsx`
  - calls `POST: /api/purchase-requests/:id/approve`
  - update the page on success
- Render an approve button
  - pass in `handleApproveRequest()` to `onClick()`
  - disable the button if the request does not require my approval

## Part 3: filter by status

- In `App.tsx`, render `<FilterByStatus />` under `<ListRequests />`
- Update `FilterByStatus.tsx` to render dropdown options for each possible purchase request status, as well as ALL
- On select, filter the list of requests shown by that status
  - when ALL is selected, show all purchase requests

### If time permits:

- Loading state
- Basic error handling
- Styling
- Unit tests

## PROJECT STRUCTURE

- `/src/App.tsx`: the file housing your root component.
- `/src/components/` the folder housing your helper components.
- `/src/tests/App.spec.tsx`: optional test file you can flesh out if time permits.
- `/package.json`: if you choose to add new dependencies, you can do so in terminal.

import { useEffect, useState } from "react";

type ApiProbe = {
  status: number;
  body: string;
};

export default function App() {
  const [probe, setProbe] = useState<ApiProbe | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch("/api/purchase-requests/")
      .then(async (response) => {
        setProbe({ status: response.status, body: await response.text() });
      })
      .catch((reason: unknown) => setError(String(reason)));
  }, []);

  return (
    <main>
      <h1>Purchase Requests</h1>
      <p>See EXERCISE.md for the brief. Replace what follows.</p>
      {error && <pre className="probe">{error}</pre>}
      {probe && (
        <pre className="probe">
          GET /api/purchase-requests/ {"→"} {probe.status}
          {"\n"}
          {probe.body}
        </pre>
      )}
    </main>
  );
}

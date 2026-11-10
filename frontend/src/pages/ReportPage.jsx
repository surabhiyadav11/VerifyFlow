import { Link, useParams } from "react-router-dom";

export default function ReportPage() {
  const { id } = useParams();
  return (
    <section className="page-container">
      <h1>Validation Report</h1>
      <p>Check ID: {id} (placeholder)</p>
      <Link to={`/checks/${id}/review`}>Back to Review</Link>
    </section>
  );
}


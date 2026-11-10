import { Link, useParams } from "react-router-dom";

export default function ReviewPage() {
  const { id } = useParams();
  return (
    <section className="page-container">
      <h1>Review &amp; Edit Extracted Fields</h1>
      <p>Check ID: {id} (placeholder)</p>
      <Link to={`/checks/${id}/report`}>Continue to Report</Link>
    </section>
  );
}


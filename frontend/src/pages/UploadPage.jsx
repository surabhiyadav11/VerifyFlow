import { Link, useParams } from "react-router-dom";

export default function UploadPage() {
  const { id } = useParams();
  return (
    <section className="page-container">
      <h1>Upload Documents</h1>
      <p>Check ID: {id} (placeholder)</p>
      <Link to={`/checks/${id}/review`}>Continue to Review</Link>
    </section>
  );
}


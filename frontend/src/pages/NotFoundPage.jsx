import { Link } from "react-router-dom";

export default function NotFoundPage() {
  return (
    <section className="page-container">
      <h1>404 — Page Not Found</h1>
      <p>The requested page does not exist.</p>
      <Link to="/">Back to Home</Link>
    </section>
  );
}


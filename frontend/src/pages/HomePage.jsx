import { Link } from "react-router-dom";

export default function HomePage() {
  return (
    <section className="page-container">
      <h1>VerifyFlow</h1>
      <p>Choose a document verification type (placeholder).</p>
      <div className="placeholder-links">
        <Link to="/checks/demo/upload">Go to Upload Page</Link>
      </div>
    </section>
  );
}


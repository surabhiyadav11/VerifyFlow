import { Routes, Route, Link } from "react-router-dom";
import HomePage from "./pages/HomePage.jsx";
import UploadPage from "./pages/UploadPage.jsx";
import ReviewPage from "./pages/ReviewPage.jsx";
import ReportPage from "./pages/ReportPage.jsx";
import HistoryPage from "./pages/HistoryPage.jsx";
import NotFoundPage from "./pages/NotFoundPage.jsx";

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <Link to="/" className="brand-link">
          VerifyFlow
        </Link>
        <nav className="app-nav">
          <Link to="/">Home</Link>
          <Link to="/checks/demo/upload">Upload</Link>
          <Link to="/checks/demo/review">Review</Link>
          <Link to="/checks/demo/report">Report</Link>
          <Link to="/history">History</Link>
        </nav>
      </header>
      <main className="app-main">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/checks/:id/upload" element={<UploadPage />} />
          <Route path="/checks/:id/review" element={<ReviewPage />} />
          <Route path="/checks/:id/report" element={<ReportPage />} />
          <Route path="/history" element={<HistoryPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
    </div>
  );
}


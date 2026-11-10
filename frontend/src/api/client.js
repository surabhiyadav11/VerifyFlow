const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000/api";

async function request(path, options = {}) {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    headers: {
      ...(options.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    let errorData;
    try {
      errorData = await response.json();
    } catch {
      errorData = { error: { code: "HTTP_ERROR", message: response.statusText } };
    }
    throw errorData;
  }

  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const apiClient = {
  getHealth: () => request("/health"),
  createCheck: (docType) =>
    request("/checks", { method: "POST", body: JSON.stringify({ doc_type: docType }) }),
  listChecks: () => request("/checks"),
  getCheck: (checkId) => request(`/checks/${checkId}`),
  deleteCheck: (checkId) => request(`/checks/${checkId}`, { method: "DELETE" }),
  uploadDocument: (checkId, formData) =>
    request(`/checks/${checkId}/documents`, { method: "POST", body: formData }),
  updateDocumentFields: (checkId, documentId, fields) =>
    request(`/checks/${checkId}/documents/${documentId}`, {
      method: "PATCH",
      body: JSON.stringify({ fields }),
    }),
  validateCheck: (checkId) =>
    request(`/checks/${checkId}/validate`, { method: "POST" }),
  getReport: (checkId) => request(`/checks/${checkId}/report`),
  getRules: () => request("/rules"),
};


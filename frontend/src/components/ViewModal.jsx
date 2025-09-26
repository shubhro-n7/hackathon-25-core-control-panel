import React, { useEffect, useState } from "react";
import { Button } from "antd";
import { apiCall } from "../utils/api";

const ViewModal = ({ open, onClose, viewId }) => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState("");
    const [error, setError] = useState("");

    useEffect(() => {
        if (!open || !viewId) return;
        setLoading(true);
        setError("");
        setData("");
        apiCall(`/views/${viewId}`)
            .then((res) => {
                setData(JSON.stringify(res, null, 2));
                setLoading(false);
            })
            .catch(() => {
                setError("Failed to fetch view details");
                setLoading(false);
            });
    }, [open, viewId]);

    if (!open) return null;
    return (
        <div
            style={{
                position: "fixed",
                top: 0,
                left: 0,
                width: "100vw",
                height: "100vh",
                background: "rgba(0,0,0,0.3)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                zIndex: 1000,
            }}
        >
            <div
                style={{
                    background: "#fff",
                    padding: 32,
                    borderRadius: 8,
                    minWidth: 500,
                    maxWidth: 700,
                    boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
                }}
            >
                <h2>View Details</h2>
                {loading ? (
                    <div>Loading...</div>
                ) : error ? (
                    <div style={{ color: "red" }}>{error}</div>
                ) : (
                    <pre style={{
                        background: "#f5f5f5",
                        padding: 16,
                        borderRadius: 4,
                        maxHeight: 400,
                        overflow: "auto",
                        fontSize: 14,
                    }}>{data}</pre>
                )}
                <div style={{ display: "flex", justifyContent: "flex-end", marginTop: 16 }}>
                    <Button onClick={onClose}>Close</Button>
                </div>
            </div>
        </div>
    );
};

export default ViewModal;

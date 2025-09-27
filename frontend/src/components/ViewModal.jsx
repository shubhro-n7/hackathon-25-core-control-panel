import React, { useEffect, useState } from "react";
import { Button, Select, message } from "antd";
import { CloseOutlined } from "@ant-design/icons";
import { apiCall } from "../utils/api";


const ViewModal = ({ open, onClose, viewId, handleActivate, envs, selectedEnv }) => {
    const [loading, setLoading] = useState(false);
    const [data, setData] = useState("");
    const [error, setError] = useState("");
    const [selectedEnvs, setSelectedEnvs] = useState([]);
    const [copyLoading, setCopyLoading] = useState(false);

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
        setSelectedEnvs([]);
    }, [open, viewId]);

    if (!open) return null;
    const handleCopy = async () => {
        if (!viewId || selectedEnvs.length === 0) {
            message.error("Select at least one environment");
            return;
        }
        setCopyLoading(true);
        try {
            const res = await apiCall("/views/copy", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ viewId, envIds: selectedEnvs }),
            });
            message.success(res.message || "Copied successfully");
            setSelectedEnvs([]);
            onClose();
        } catch (err) {
            message.error(err.message || "Copy failed");
        } finally {
            setCopyLoading(false);
        }
    };

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
                    position: "relative",
                }}
            >
                <Button
                    type="text"
                    icon={<CloseOutlined style={{ fontSize: 20 }} />}
                    onClick={onClose}
                    style={{
                        position: "absolute",
                        top: 16,
                        right: 16,
                        zIndex: 10,
                    }}
                    aria-label="Close"
                />
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
                <div style={{ marginTop: 16 }}>
                    <div style={{ marginBottom: 12 }}>
                        <label><b>Copy to Environments:</b></label>
                        <Select
                            mode="multiple"
                            style={{ width: "100%", marginTop: 8 }}
                            placeholder="Select environments"
                            value={selectedEnvs}
                            onChange={setSelectedEnvs}
                            options={envs.map((env) => ({ label: env.envName, value: env.id, disabled: env.id === selectedEnv }))}
                        />
                    </div>
                    <div style={{ display: "flex", justifyContent: "flex-end", gap: 8 }}>
                        {data && <Button type="primary" loading={copyLoading} onClick={handleCopy} disabled={selectedEnvs.length === 0}>
                            Copy
                        </Button>}
                        {data && <Button type="default" onClick={() => handleActivate(JSON.parse(data))}>
                            Activate
                        </Button>}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ViewModal;

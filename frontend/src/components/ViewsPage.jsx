import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Select, Table, Button, Space } from "antd";
import ViewModal from "./ViewModal";
import { apiCall } from "../utils/api";

const ViewsPage = () => {
    const { envId } = useParams();
    const [envs, setEnvs] = useState([]);
    const [selectedEnv, setSelectedEnv] = useState(envId || "");
    const navigate = useNavigate();

    const [views, setViews] = useState([]);
    const [modalOpen, setModalOpen] = useState(false);
    const [viewModalOpen, setViewModalOpen] = useState(false);
    const [viewModalId, setViewModalId] = useState("");
    const [viewData, setViewData] = useState("");
    const [jsonError, setJsonError] = useState("");


    useEffect(() => {
            apiCall("/envs")
                .then((data) => setEnvs(data))
                .catch(() => {
                    setEnvs([]);
                });
    }, []);
    useEffect(() => {
        setSelectedEnv(envId || "");
    }, [envId]);

    const loadVewsByEnv = async (envId) => {
            try {
                const data = await apiCall(`/views/env/${envId}`);
                setViews(data.views || []);
            } catch (err) {
                console.error(err);
                setViews([]);
            }
    };

    useEffect(() => {
        if (selectedEnv) {
            loadVewsByEnv(selectedEnv);
        } else {
            setViews([]);
        }
    }, [selectedEnv]);

    // Activate view and refresh table
    const handleActivate = async (record) => {
            if (!record || !record.key) return;
            try {
                await apiCall(`/views/${record.key}/activate`, {
                    method: "PUT",
                });
                // Refresh views list
                loadVewsByEnv(selectedEnv);
            } catch (err) {
                alert("Failed to activate view");
            }
    };

    // View details handler
    const handleViewDetails = (record) => {
        if (!record || !record.key) return;
        setViewModalId(record.key);
        setViewModalOpen(true);
    };

    // Create view handler
    const handleCreateView = async () => {
        setJsonError("");
        let parsed;
        try {
            parsed = JSON.parse(viewData);
        } catch (e) {
            setJsonError("Invalid JSON");
            return;
        }
        try {
            await apiCall("/views", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    envId: selectedEnv,
                    viewData: parsed,
                }),
            });
            setModalOpen(false);
            setViewData("");
            loadVewsByEnv(selectedEnv);
        } catch (err) {
            setJsonError("Failed to create view");
        }
    };

    return (
        <div style={{ padding: "2rem" }}>
            <h2>Select Environment</h2>
            <div style={{ maxWidth: 300 }}>
                <Select
                    value={selectedEnv}
                    onChange={(value) => navigate(`/views/${value}`)}
                    style={{ width: "100%" }}
                    placeholder="-- Select --"
                >
                    {envs.map((env) => (
                        <Select.Option key={env.id} value={env.id}>
                            {env.envName}
                        </Select.Option>
                    ))}
                </Select>
            </div>
            {selectedEnv && (
                <div style={{ marginTop: "2rem" }}>
                    <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                        <h3>Views for Environment ID: {selectedEnv}</h3>
                        <Button type="primary" onClick={() => setModalOpen(true)}>
                            Create View
                        </Button>
                    </div>
                    <Table
                        dataSource={views.map((view) => ({
                            key: view.id,
                            name: view.name,
                            status: view.status,
                            createdAt: view.createdAt,
                        }))}
                        columns={[
                            {
                                title: "Name",
                                dataIndex: "name",
                                key: "name",
                            },
                            {
                                title: "Status",
                                dataIndex: "status",
                                key: "status",
                            },
                            {
                                title: "Created At",
                                dataIndex: "createdAt",
                                key: "createdAt",
                                render: (text) => text ? new Date(text).toLocaleString() : "-",
                            },
                            {
                                title: "Actions",
                                key: "actions",
                                render: (_, record) => (
                                    <Space size="middle">
                                        <Button type="link" onClick={() => handleActivate(record)}>
                                            Activate
                                        </Button>
                                        <Button type="link" onClick={() => handleViewDetails(record)}>
                                            View
                                        </Button>
                                    </Space>
                                ),
                            },
                        ]}
                        pagination={false}
                        locale={{ emptyText: "No views found for this environment." }}
                    />
                    {/* Modal for Create View */}
                    {modalOpen && (
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
                                <h2>Create View</h2>
                                <textarea
                                    value={viewData}
                                    onChange={(e) => setViewData(e.target.value)}
                                    style={{ width: "100%", height: 200, fontSize: 16, marginBottom: 16 }}
                                    placeholder="Paste JSON view data here"
                                />
                                {jsonError && <div style={{ color: "red", marginBottom: 8 }}>{jsonError}</div>}
                                <div style={{ display: "flex", gap: 16, justifyContent: "flex-end" }}>
                                    <Button onClick={() => { setModalOpen(false); setViewData(""); setJsonError(""); }}>
                                        Cancel
                                    </Button>
                                    <Button type="primary" onClick={handleCreateView}>
                                        Submit
                                    </Button>
                                </div>
                            </div>
                        </div>
                    )}
                    {/* Modal for View Details */}
                    <ViewModal
                        open={viewModalOpen}
                        onClose={() => setViewModalOpen(false)}
                        viewId={viewModalId}
                    />
                </div>
            )}
        </div>
    );
};

export default ViewsPage;
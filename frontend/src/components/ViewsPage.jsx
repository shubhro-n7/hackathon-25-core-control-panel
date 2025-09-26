import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Select, Table, Button, Space } from "antd";
import { apiCall } from "../utils/api";

const ViewsPage = () => {
    const { envId } = useParams();
    const [envs, setEnvs] = useState([]);
    const [selectedEnv, setSelectedEnv] = useState(envId || "");
    const navigate = useNavigate();

    const [views, setViews] = useState([]);


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
                    <h3>Views for Environment ID: {selectedEnv}</h3>
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
                                    </Space>
                                ),
                            },
                        ]}
                        pagination={false}
                        locale={{ emptyText: "No views found for this environment." }}
                    />
                </div>
            )}
        </div>
    );
};

export default ViewsPage;
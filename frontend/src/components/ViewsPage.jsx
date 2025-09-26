import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { Select } from "antd";

const ViewsPage = () => {
    const { envId } = useParams();
    const [envs, setEnvs] = useState([]);
    const [selectedEnv, setSelectedEnv] = useState(envId || "");
    const navigate = useNavigate();


    useEffect(() => {
        fetch("http://localhost:8000/envs")
            .then((res) => res.json())
            .then((data) => setEnvs(data))
            .catch((err) => {
                setEnvs([]);
            });
    }, []);
    useEffect(() => {
        setSelectedEnv(envId || "");
    }, [envId]);

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
                    {/* Placeholder for views content */}
                    <p>Views content goes here...</p>
                </div>
            )}
        </div>
    );
};

export default ViewsPage;
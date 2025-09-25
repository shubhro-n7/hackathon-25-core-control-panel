import React, { useEffect, useState } from "react";
import { Table, Space, Button, message } from "antd";
import { useNavigate } from "react-router-dom";

const EnvTablePage = () => {
  const [envs, setEnvs] = useState([]);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Columns definition for Antd Table
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Name",
      dataIndex: "envName",
      key: "envName",
    },
    {
      title: "Slug",
      dataIndex: "slug",
      key: "slug",
    },
    {
      title: "Description",
      dataIndex: "description",
      key: "description",
    },
    {
      title: "Created By",
      dataIndex: "createdBy",
      key: "createdBy",
    },
    {
      title: "Created At",
      dataIndex: "createdAt",
      key: "createdAt",
      render: (text) => new Date(text).toLocaleString(),
    },
    {
      title: "Action",
      key: "action",
      render: (_, record) => (
        <Space size="middle">
          <Button type="link" onClick={() => handleView(record)}>
            View
          </Button>
        </Space>
      ),
    },
  ];

  // Handler for action
  const handleView = (record) => {
    navigate(`/envs/${record.id}`);
  };


  const fetchEnvs = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/envs"); // Adjust backend URL
      if (!res.ok) throw new Error("Failed to fetch envs");
      const data = await res.json();
      setEnvs(data);
    } catch (err) {
      console.error(err);
      message.error("Error fetching environments");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchEnvs();
  }, []);

  return (
    <div style={{ padding: "24px" }}>
      <h2>All Environments</h2>
      <Table
        columns={columns}
        dataSource={envs.map((e) => ({ ...e, key: e.id }))}
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
    </div>
  );
};

export default EnvTablePage;

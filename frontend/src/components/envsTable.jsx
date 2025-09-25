import React, { useEffect, useState } from "react";
import { Table, Space, Button, message, Modal, Form, Input } from "antd";
import { useNavigate } from "react-router-dom";

const EnvTablePage = () => {
  const [envs, setEnvs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [modalLoading, setModalLoading] = useState(false);
  const [modalError, setModalError] = useState("");
  const [form] = Form.useForm();
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

  // Handler for modal open
  const handleOpenModal = () => {
    setModalVisible(true);
    setModalError("");
    form.resetFields();
  };

  // Handler for modal close
  const handleCloseModal = () => {
    setModalVisible(false);
    setModalError("");
    form.resetFields();
  };

  // Handler for form submit
  const handleCreateEnv = async () => {
    try {
      setModalLoading(true);
      setModalError("");
      const values = await form.validateFields();
      const res = await fetch("http://localhost:8000/envs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(values),
      });
      if (!res.ok) {
        const errData = await res.json();
        setModalError(errData.detail || "Failed to create environment");
        setModalLoading(false);
        return;
      }
      message.success("Environment created successfully");
      setModalVisible(false);
      fetchEnvs();
    } catch (err) {
      if (err.errorFields) {
        setModalError("Please fill all required fields.");
      } else {
        setModalError("Error creating environment");
      }
    } finally {
      setModalLoading(false);
    }
  };

  return (
    <div style={{ padding: "24px" }}>
      <h2>All Environments</h2>
      <Button type="primary" style={{ marginBottom: 16 }} onClick={handleOpenModal}>
        Create Env
      </Button>
      <Table
        columns={columns}
        dataSource={envs.map((e) => ({ ...e, key: e.id }))}
        loading={loading}
        pagination={{ pageSize: 10 }}
      />
      <Modal
        title="Create Environment"
        open={modalVisible}
        onCancel={handleCloseModal}
        onOk={handleCreateEnv}
        confirmLoading={modalLoading}
        okText="Create"
      >
        <Form form={form} layout="vertical">
          <Form.Item
            label="Environment Name"
            name="envName"
            rules={[{ required: true, message: "Please enter environment name" }]}
          >
            <Input placeholder="e.g. Staging" />
          </Form.Item>
          <Form.Item
            label="Slug"
            name="slug"
            rules={[{ required: true, message: "Please enter slug" }]}
          >
            <Input placeholder="e.g. staging" />
          </Form.Item>
          <Form.Item
            label="Description"
            name="description"
            rules={[{ required: true, message: "Please enter description" }]}
          >
            <Input placeholder="Description" />
          </Form.Item>
          <Form.Item
            label="Created By"
            name="createdBy"
            rules={[{ required: true, message: "Please enter creator name" }]}
          >
            <Input placeholder="Your name" />
          </Form.Item>
        </Form>
        {modalError && (
          <div style={{ color: "red", marginTop: 8 }}>{modalError}</div>
        )}
      </Modal>
    </div>
  );
};

export default EnvTablePage;

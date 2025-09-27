import React, { useEffect, useState } from "react";
import { Table, Space, Button, message, Card, Modal } from "antd";
import { useParams } from "react-router-dom";
import { apiCall } from "../utils/api";

const EnvDetailPage = () => {
  const { envId } = useParams();
  const [env, setEnv] = useState(null);
  const [keys, setKeys] = useState([]);
  const [loading, setLoading] = useState(false);
  const [creatingKey, setCreatingKey] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [modalData, setModalData] = useState(null);

  // Columns for EnvKeys Table
  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
    },
    {
      title: "Status",
      dataIndex: "status",
      key: "status",
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
        <Space>

          <Button
            type="link"
            disabled={record.status === "active" || record.status === "revoked"}
            onClick={async () => {
                try {
                  await apiCall(`/envs/keys/${record.id}/activate`, { method: "POST" });
                  message.success("Key activated");
                  fetchKeys();
                } catch (err) {
                  message.error("Error activating key");
                }
            }}
          >
            Activate
          </Button>
          <Button
            type="link"
            disabled={record.status === "inactive" || record.status === "revoked"}
            onClick={async () => {
                try {
                  await apiCall(`/envs/keys/${record.id}/pause`, { method: "POST" });
                  message.success("Key paused (inactive)");
                  fetchKeys();
                } catch (err) {
                  message.error("Error pausing key");
                }
            }}
          >
            Pause
          </Button>
          <Button
            type="link"
            danger
            disabled={record.status === "revoked"}
            onClick={async () => {
                try {
                  await apiCall(`/envs/keys/${record.id}/expire`, { method: "POST" });
                  message.success("Key expired (revoked)");
                  fetchKeys();
                } catch (err) {
                  message.error("Error expiring key");
                }
            }}
          >
            Expire
          </Button>
        </Space>
      ),
    },
  ];

  const fetchEnv = async () => {
      try {
        const data = await apiCall(`/envs`);
        const selectedEnv = data.find((e) => e.id === envId);
        setEnv(selectedEnv || null);
      } catch (err) {
        console.error(err);
        message.error("Error fetching environment");
      }
  };

  const fetchKeys = async () => {
    setLoading(true);
    try {
    const data = await apiCall(`/envs/envKeys?envId=${envId}`);
    setKeys(data);
    } catch (err) {
      console.error(err);
      message.error("Error fetching keys");
    } finally {
      setLoading(false);
    }
  };

  const createKey = async () => {
    setCreatingKey(true);
    try {
        const data = await apiCall(
          `/envs/${envId}/keys?createdBy=shubhro`,
          { method: "POST" }
        );
        setModalData(data);
        setModalVisible(true);
        fetchKeys(); // Refresh table
    } catch (err) {
      console.error(err);
      message.error("Error creating key");
    } finally {
      setCreatingKey(false);
    }
  };

  useEffect(() => {
    fetchEnv();
    fetchKeys();
  }, [envId]);

  if (!env) return <div>Loading environment...</div>;

  return (
    <div style={{ padding: "24px" }}>
      <Card title={`Environment: ${env.envName}`} style={{ marginBottom: 24 }}>
        <p><b>Slug:</b> {env.slug}</p>
        <p><b>Description:</b> {env.description}</p>
        <p><b>Created By:</b> {env.createdBy}</p>
        <p><b>Created At:</b> {new Date(env.createdAt).toLocaleString()}</p>
      </Card>

      <Space style={{ marginBottom: 16 }}>
        <Button type="primary" onClick={createKey} loading={creatingKey}>
          Generate New Key
        </Button>
      </Space>

      <Table
        columns={columns}
        dataSource={keys.map((k) => ({ ...k, key: k.id }))}
        loading={loading}
        pagination={{ pageSize: 10 }}
        title={() => "Environment Keys"}
      />

      <Modal
        visible={modalVisible}
        title="New Key Created"
        onCancel={() => setModalVisible(false)}
        footer={[
          <Button key="close" type="primary" onClick={() => setModalVisible(false)}>
            Close
          </Button>,
        ]}
      >
        {modalData && (
          <div>
            <p><b>Secret:</b> {modalData.secret}</p>
            <p><b>Env ID:</b> {modalData.envId}</p>
          </div>
        )}
      </Modal>
    </div>
  );
};

export default EnvDetailPage;

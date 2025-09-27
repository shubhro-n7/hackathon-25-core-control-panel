import React, { useEffect, useState } from "react";
import { apiCall } from "../utils/api";
import { Form, Input, Button, Select, Space, Card, message } from "antd";
import { CloseOutlined } from "@ant-design/icons";

// Dynamic options from API
const entityFields = [

    { name: "order", label: "Order", type: "number" }
];

const ViewEditForm = ({ initialValues, onCancel, selectedEnv, disabled }) => {
    const [menuOptions, setMenuOptions] = useState([]);
    const [entityOptions, setEntityOptions] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        apiCall("/views/menus/all")
            .then((res) => {
                setMenuOptions(
                    (res.menus || []).map((m) => ({ label: m.label, value: m.name, id: m.id }))
                );
                setEntityOptions(
                    (res.submenus || []).map((sm) => ({ label: sm.label, value: sm.name, id: sm.id }))
                );
                setLoading(false);
            })
            .catch(() => {
                setMenuOptions([]);
                setEntityOptions([]);
                setLoading(false);
            });
    }, []);

    const handleSubmit = async (values) => {
        try {
            // Transform payload
            const transformed = {
                viewId: values.id,
                name: values.name,
                menus: (values.menus || []).map((menu) => {
                    const menuObj = menuOptions.find((m) => m.name === menu.name || m.value === menu.name);
                    return {
                        id: menuObj?.id || menu.name,
                        order: menu.order,
                        entities: (menu.entities || []).map((entity) => {
                            const entityObj = entityOptions.find((e) => e.name === entity.name || e.value === entity.name);
                            return {
                                id: entityObj?.id || entity.name,
                                order: entity.order
                            };
                        })
                    };
                })
            };
            const payload = {
                envId: selectedEnv,
                viewData: transformed
            };
            const res = await apiCall("/views/create/", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload),
            });
            message.success(res.message || "View created successfully");
            if (onCancel) onCancel();
            window.location.reload();
        } catch (err) {
            message.error(err.message || "Failed to create view");
        }
    };

    return (
        <div style={{ maxHeight: 500, overflowY: "auto", paddingRight: 8 }}>
            {loading ? (
                <div>Loading menu options...</div>
            ) : (
                <Form
                    layout="vertical"
                    initialValues={initialValues}
                    onFinish={handleSubmit}
                    autoComplete="off"
                >
                    <Form.Item name="id" label="ID" rules={[{ required: true, message: "ID is required" }]}> 
                        <Input type="number" disabled={disabled} />
                    </Form.Item>
                    <Form.Item name="name" label="View Name" rules={[{ required: true, message: "Name is required" }]}> 
                        <Input disabled={disabled} />
                    </Form.Item>
                    <Form.List name="menus">
                        {(fields, { add, remove }) => (
                            <div>
                                {fields.map((field, idx) => (
                                    <Card
                                        key={field.key}
                                        style={{
                                            marginBottom: 16,
                                            position: "relative",
                                            paddingTop: 16,
                                            background: "#f0f2f5",
                                            border: "1px solid #e0e0e0"
                                        }}
                                        bodyStyle={{ paddingTop: 8, background: "#f0f2f5" }}
                                    >
                                        {!disabled && (
                                            <Button
                                                type="text"
                                                icon={<CloseOutlined />}
                                                onClick={() => remove(field.name)}
                                                style={{ position: "absolute", top: 4, right: 4, zIndex: 2, color: "#888" }}
                                                size="small"
                                                aria-label="Remove Menu"
                                            />
                                        )}
                                        <Form.Item
                                            {...field}
                                            name={[field.name, "name"]}
                                            label="Menu Name"
                                            rules={[{ required: true, message: "Menu name required" }]}
                                        >
                                            <Select options={menuOptions} showSearch disabled={disabled} />
                                        </Form.Item>
                                        <Form.List name={[field.name, "entities"]}>
                                            {(entityFieldsArr, { add: addEntity, remove: removeEntity }) => (
                                                <div>
                                                    {entityFieldsArr.map((entityField, eIdx) => (
                                                        <Card
                                                            key={entityField.key}
                                                            size="small"
                                                            style={{ marginBottom: 8, position: "relative", paddingTop: 12 }}
                                                            bodyStyle={{ paddingTop: 8 }}
                                                        >
                                                            {!disabled && (
                                                                <Button
                                                                    type="text"
                                                                    icon={<CloseOutlined />}
                                                                    onClick={() => removeEntity(entityField.name)}
                                                                    style={{ position: "absolute", top: 2, right: 2, zIndex: 2, color: "#888" }}
                                                                    size="small"
                                                                    aria-label="Remove Entity"
                                                                />
                                                            )}
                                                            <Form.Item
                                                                {...entityField}
                                                                name={[entityField.name, "name"]}
                                                                label="Entity Name"
                                                                rules={[{ required: true, message: "Entity name required" }]}
                                                            >
                                                                <Select options={entityOptions} showSearch disabled={disabled} />
                                                            </Form.Item>
                                                            {entityFields.map((ef) => (
                                                                <Form.Item
                                                                    key={ef.name}
                                                                    {...entityField}
                                                                    name={[entityField.name, ef.name]}
                                                                    label={ef.label}
                                                                    valuePropName={ef.type === "checkbox" ? "checked" : "value"}
                                                                >
                                                                    {ef.type === "checkbox" ? <Input type="checkbox" disabled={disabled} /> : <Input type={ef.type} disabled={disabled} />}
                                                                </Form.Item>
                                                            ))}
                                                        </Card>
                                                    ))}
                                                    {!disabled && (
                                                        <div style={{ marginBottom: 8 }}>
                                                            <Button type="dashed" onClick={() => addEntity()} block>
                                                                Add Entity
                                                            </Button>
                                                        </div>
                                                    )}
                                                </div>
                                            )}
                                        </Form.List>
                                    </Card>
                                ))}
                                {!disabled && (
                                    <Form.Item>
                                        <Button type="dashed" onClick={() => add()} block>
                                            Add Menu
                                        </Button>
                                    </Form.Item>
                                )}
                            </div>
                        )}
                    </Form.List>
                    {!disabled && (
                        <Form.Item style={{ marginTop: 24 }}>
                            <Space>
                                <Button onClick={onCancel}>Cancel</Button>
                                <Button type="primary" htmlType="submit">Save Copy</Button>
                            </Space>
                        </Form.Item>
                    )}
                </Form>
            )}
        </div>
    );
};

export default ViewEditForm;

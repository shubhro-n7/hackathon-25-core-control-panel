import React from 'react'
import { Form, Input, Button, Select, message } from 'antd'


export default function SampleForm() {
    const [form] = Form.useForm()


    const onFinish = values => {
        message.success('Form submitted: ' + JSON.stringify(values))
        form.resetFields()
    }


    return (
        <Form form={form} layout="vertical" onFinish={onFinish} style={{ maxWidth: 600 }}>
            <Form.Item name="name" label="Name" rules={[{ required: true, message: 'Please input a name' }]}>
                <Input placeholder="John Doe" />
            </Form.Item>


            <Form.Item name="role" label="Role" rules={[{ required: true }]}>
                <Select placeholder="Select role">
                    <Select.Option value="dev">Developer</Select.Option>
                    <Select.Option value="pm">Product Manager</Select.Option>
                    <Select.Option value="designer">Designer</Select.Option>
                </Select>
            </Form.Item>


            <Form.Item>
                <Button type="primary" htmlType="submit">Submit</Button>
            </Form.Item>
        </Form>
    )
}
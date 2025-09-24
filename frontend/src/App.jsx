import React from 'react'
import { Layout, Menu, Button, Space, theme } from 'antd'
import {
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
} from '@ant-design/icons'
import SampleTable from './components/SampleTable'
import SampleForm from './components/SampleForm'


const { Header, Sider, Content } = Layout


export default function App() {
  const [collapsed, setCollapsed] = React.useState(false)
  const { token } = theme.useToken()


  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
        <div style={{ height: 48, margin: 16, background: 'rgba(255,255,255,0.2)', borderRadius: 6 }} />
        <Menu theme="dark" defaultSelectedKeys={["1"]} mode="inline">
          <Menu.Item key="1" icon={<UserOutlined />}>Users</Menu.Item>
          <Menu.Item key="2" icon={<VideoCameraOutlined />}>Videos</Menu.Item>
          <Menu.Item key="3" icon={<UploadOutlined />}>Uploads</Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header style={{ padding: '0 16px', background: token.colorBgContainer }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Space>
              <Button type="text" icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />} onClick={() => setCollapsed(!collapsed)} />
              <h3 style={{ margin: 0 }}>React + Ant Design Boilerplate</h3>
            </Space>
            <Space>
              <Button>Docs</Button>
              <Button type="primary">Sign In</Button>
            </Space>
          </div>
        </Header>
        <Content style={{ margin: 16 }}>
          <div style={{ padding: 16, minHeight: 360, background: token.colorBgContainer, borderRadius: 8 }}>
            <h2>Overview</h2>
            <p>This template uses Vite + React + Ant Design (antd). Below are example components: a table and a form to get you started.</p>


            <SampleForm />


            <div style={{ height: 24 }} />


            <SampleTable />
          </div>
        </Content>
      </Layout>
    </Layout>
  )
}

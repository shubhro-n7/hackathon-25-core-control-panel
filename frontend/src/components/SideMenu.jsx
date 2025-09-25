import React from 'react'
import { Menu } from 'antd'
import {
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
} from '@ant-design/icons'
import { Link } from 'react-router-dom'

export default function SideMenu({ collapsed, onCollapse }) {
  return (
    <div>
      <div style={{ height: 48, margin: 16, background: 'rgba(255,255,255,0.2)', borderRadius: 6 }} />
      <Menu theme="dark" defaultSelectedKeys={["1"]} mode="inline">
        <Menu.Item key="1" icon={<UserOutlined />}>
          <Link to="/envs">Envs</Link>
        </Menu.Item>
        <Menu.Item key="2" icon={<VideoCameraOutlined />}>
          <Link to="/videos">Videos</Link>
        </Menu.Item>
        <Menu.Item key="3" icon={<UploadOutlined />}>
          <Link to="/uploads">Uploads</Link>
        </Menu.Item>
      </Menu>
    </div>
  )
}

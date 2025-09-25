import React from 'react'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Layout, theme } from 'antd'
import SideMenu from './components/SideMenu'
import ItemTable from './components/ItemTable'
import EnvTable from './components/envsTable'
import EnvDetailPage from './components/envDetail'
// Placeholder components for Videos and Uploads
const Videos = () => <div style={{ padding: 16 }}>Videos Page</div>
const Uploads = () => <div style={{ padding: 16 }}>Uploads Page</div>


const { Sider, Content } = Layout


export default function App() {
  const [collapsed, setCollapsed] = React.useState(false)
  const { token } = theme.useToken()

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider collapsible collapsed={collapsed} onCollapse={setCollapsed}>
          <SideMenu collapsed={collapsed} onCollapse={setCollapsed} />
        </Sider>
        <Layout>
          <Content style={{ margin: 16 }}>
            <Routes>
              <Route path="/envs" element={<EnvTable />} />
              <Route path="/envs/:envId" element={<EnvDetailPage />} />
              <Route path="/items" element={<ItemTable />} />
              <Route path="/videos" element={<Videos />} />
              <Route path="/uploads" element={<Uploads />} />
              <Route path="/" element={<ItemTable />} />
            </Routes>
          </Content>
        </Layout>
      </Layout>
    </Router>
  )
}

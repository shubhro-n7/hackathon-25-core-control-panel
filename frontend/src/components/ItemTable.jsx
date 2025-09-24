import React from 'react'
import { Table } from 'antd'

const columns = [
    { title: 'Name', dataIndex: 'name', key: 'name' },
    { title: 'Description', dataIndex: 'description', key: 'description' },
    { title: 'Price', dataIndex: 'price', key: 'price', render: price => `$${price}` },
    { 
        title: 'Created At', 
        dataIndex: 'created_at', 
        key: 'created_at',
        render: created_at => {
            const date = new Date(created_at);
            return date.toLocaleString();
        }
    },
]



export default function ItemTable() {
    const [data, setData] = React.useState([]);

    const [loading, setLoading] = React.useState(false);

    React.useEffect(() => {
        setLoading(true);
        fetch('http://localhost:8000/items/')
            .then(response => response.json())
            .then(items => setData(items))
            .catch(error => console.error('Error fetching items:', error))
            .finally(() => setLoading(false));
    }, []);
    return <Table columns={columns} dataSource={data} pagination={{ pageSize: 5 }} />
}
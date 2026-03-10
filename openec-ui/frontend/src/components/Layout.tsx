import { NavLink, Outlet } from 'react-router-dom'
import {
  LayoutDashboard, Package, ShoppingCart, Users,
  Box, TrendingUp, BarChart2, DollarSign, FileText,
  Menu, X,
} from 'lucide-react'
import { useState } from 'react'

const NAV_ITEMS = [
  { name: 'Overview', path: '/', icon: LayoutDashboard },
  { name: 'Products', path: '/products', icon: Package },
  { name: 'Orders', path: '/orders', icon: ShoppingCart },
  { name: 'Customers', path: '/customers', icon: Users },
  { name: 'Inventory', path: '/inventory', icon: Box },
  { name: 'Marketing', path: '/marketing', icon: TrendingUp },
  { name: 'Analytics', path: '/analytics', icon: BarChart2 },
  { name: 'Pricing', path: '/pricing', icon: DollarSign },
]

export default function Layout() {
  const [sidebarOpen, setSidebarOpen] = useState(false)

  return (
    <div className="flex h-screen bg-gray-50">
      {/* Mobile overlay */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside className={`
        fixed lg:static inset-y-0 left-0 z-30
        w-64 bg-gray-900 text-white flex flex-col
        transform transition-transform duration-200
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
      `}>
        <div className="p-5 border-b border-gray-700">
          <h1 className="text-xl font-bold tracking-tight">OpenEC</h1>
          <p className="text-xs text-gray-400 mt-1">Ecommerce Analytics</p>
        </div>
        <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
          {NAV_ITEMS.map(item => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              onClick={() => setSidebarOpen(false)}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                }`
              }
            >
              <item.icon size={18} />
              {item.name}
            </NavLink>
          ))}
          <hr className="border-gray-700 my-3" />
          <a
            href="/docs"
            target="_blank"
            rel="noopener"
            className="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-gray-400 hover:text-white"
          >
            <FileText size={18} />
            API Docs
          </a>
        </nav>
        <div className="p-4 border-t border-gray-700 text-xs text-gray-500">
          v0.1.0
        </div>
      </aside>

      {/* Main area */}
      <div className="flex-1 flex flex-col min-w-0">
        <header className="bg-white border-b px-4 lg:px-6 py-3 flex items-center justify-between shrink-0">
          <button
            className="lg:hidden p-1 rounded hover:bg-gray-100"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          <div className="flex items-center gap-3 ml-auto">
            <select
              className="text-sm border border-gray-300 rounded-md px-2 py-1.5 bg-white"
              defaultValue="demo"
            >
              <option value="demo">Demo Provider</option>
            </select>
          </div>
        </header>
        <main className="flex-1 overflow-y-auto p-4 lg:p-6">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

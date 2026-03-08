import React from 'react'
import { Outlet } from 'react-router-dom'

export const PublicLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <div className="flex flex-col">
        <main className="flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  )
}

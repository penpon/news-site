// components/Sidebar.js
import React from "react";
import { NavLink } from "react-router-dom";
import "./Sidebar.css";

const Sidebar = () => {
  return (
    <div className="sidebar">
      <h2 className="sidebar-title">メニュー</h2>
      <nav>
        <ul className="menu">
          <li>
            <NavLink to="/" className={({ isActive }) => (isActive ? 'active' : '')}>
                ホーム
            </NavLink>
          </li>
          <li>
            <NavLink to="/articles" className={({ isActive }) => (isActive ? 'active' : '')}>
              新着記事一覧
            </NavLink>
          </li>
          <li>
            <NavLink to="/papers" className={({ isActive }) => (isActive ? 'active' : '')}>
              新着論文一覧
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;

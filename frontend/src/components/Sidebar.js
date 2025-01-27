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
            <NavLink to="/" className="menu-item" activeClassName="active">
              ホーム
            </NavLink>
          </li>
          <li>
            <NavLink to="/articles" className="menu-item" activeClassName="active">
              新着記事一覧
            </NavLink>
          </li>
          <li>
            <NavLink to="/papers" className="menu-item" activeClassName="active">
              新着論文一覧
            </NavLink>
          </li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;

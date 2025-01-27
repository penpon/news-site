// Sidebar.js
import React from "react";
import { Link } from "react-router-dom";
import { AiOutlineHome, AiOutlineFile } from "react-icons/ai";

const Sidebar = () => {
  const menuItems = [
    { name: "ホーム", icon: <AiOutlineHome />, path: "/" },
    { name: "新着記事一覧", icon: <AiOutlineFile />, path: "/articles" },
    { name: "新着論文一覧", icon: <AiOutlineFile />, path: "/papers" },
  ];

  return (
    <div style={styles.sidebar}>
      <h2 style={styles.title}>ぺんぽんNote</h2>
      <ul style={styles.menu}>
        {menuItems.map((item, index) => (
          <li key={index} style={styles.menuItem}>
            <Link to={item.path} style={styles.link}>
              {item.icon} {item.name}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
};

const styles = {
  sidebar: {
    width: "250px",
    height: "100vh",
    backgroundColor: "#2c3e50",
    color: "#ecf0f1",
    padding: "20px",
    position: "fixed",
  },
  title: {
    marginBottom: "30px",
  },
  menu: {
    listStyle: "none",
    padding: 0,
  },
  menuItem: {
    marginBottom: "15px",
  },
  link: {
    color: "#ecf0f1",
    textDecoration: "none",
    fontSize: "18px",
    display: "flex",
    alignItems: "center",
  },
};

export default Sidebar;

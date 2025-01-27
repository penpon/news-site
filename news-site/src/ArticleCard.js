// ArticleCard.js
import React from "react";

const ArticleCard = ({ title, description, link }) => {
  return (
    <div style={styles.card}>
      <h3 style={styles.title}>{title}</h3>
      <p style={styles.description}>{description}</p>
      <a href={link} target="_blank" rel="noopener noreferrer" style={styles.link}>
        続きを読む
      </a>
    </div>
  );
};

const styles = {
  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "20px",
    marginBottom: "20px",
    backgroundColor: "#fff",
    boxShadow: "0 4px 6px rgba(0, 0, 0, 0.1)",
  },
  title: {
    fontSize: "20px",
    marginBottom: "10px",
  },
  description: {
    fontSize: "16px",
    marginBottom: "10px",
    color: "#555",
  },
  link: {
    color: "#3498db",
    textDecoration: "none",
  },
};

export default ArticleCard;


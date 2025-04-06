import React from 'react';

const Footer = () => {
  return (
    <footer className="footer">
      <div className="container">
        <p>© {new Date().getFullYear()} RutaAcadémica - Sistema de Análisis de Prerrequisitos Académicos</p>
      </div>
    </footer>
  );
};

export default Footer;
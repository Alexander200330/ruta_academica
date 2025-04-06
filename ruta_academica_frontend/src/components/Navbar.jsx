import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { Navbar as BootstrapNavbar, Nav, Container } from 'react-bootstrap';

const Navbar = () => {
  return (
    <BootstrapNavbar bg="dark" variant="dark" expand="lg" sticky="top">
      <Container>
        <BootstrapNavbar.Brand as={Link} to="/">
          <div className="navbar-brand">
            <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="navbar-logo">
              <path d="M12 4L3 8L12 12L21 8L12 4Z" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M3 12L12 16L21 12" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
              <path d="M3 16L12 20L21 16" stroke="#3498db" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
            </svg>
            <span>RutaAcadémica</span>
          </div>
        </BootstrapNavbar.Brand>
        <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
        <BootstrapNavbar.Collapse id="basic-navbar-nav">
          <Nav className="ms-auto">
            <Nav.Link as={NavLink} to="/" end>
              Inicio
            </Nav.Link>
            <Nav.Link as={NavLink} to="/ruta-academica">
              Ruta Académica
            </Nav.Link>
            <Nav.Link as={NavLink} to="/about">
              Acerca de
            </Nav.Link>
          </Nav>
        </BootstrapNavbar.Collapse>
      </Container>
    </BootstrapNavbar>
  );
};

export default Navbar;
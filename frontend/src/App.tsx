import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { authService } from './services/api';
import LoginPage from './pages/LoginPage';
import JefeCarreraDashboard from './pages/JefeCarreraDashboard';
import SuperusuarioDashboard from './pages/SuperusuarioDashboard';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

function App(): any {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [usuario, setUsuario] = useState<any>(null);

  useEffect(() => {
    checkAuthentication();
  }, []);

  const checkAuthentication = async () => {
    const authenticated = authService.isAuthenticated();
    setIsAuthenticated(authenticated);
    setLoading(false);

    // Aquí podrías hacer una llamada para obtener los datos del usuario actual
    // Por simplicidad, simulamos datos del usuario
    if (authenticated) {
      setUsuario({
        id: 1,
        email: 'jefe@universidad.edu',
        nombre_completo: 'Jefe de Carrera',
        rol: 'JEFE_CARRERA',
        id_carrera: 1,
        carrera: { id: 1, nombre: 'Ingeniería en Sistemas Computacionales' }
      });
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
    checkAuthentication();
  };

  const handleLogout = () => {
    authService.logout();
    setIsAuthenticated(false);
    setUsuario(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
        <Typography>Cargando...</Typography>
      </Box>
    );
  }

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        {isAuthenticated && (
          <AppBar position="static">
            <Toolbar>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                SIGAH - {usuario?.carrera?.nombre || 'Sistema de Horarios'}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                <Typography variant="body2">
                  {usuario?.nombre_completo}
                </Typography>
                <Button color="inherit" onClick={handleLogout}>
                  Cerrar Sesión
                </Button>
              </Box>
            </Toolbar>
          </AppBar>
        )}

        <Routes>
          <Route
            path="/login"
            element={
              !isAuthenticated ? (
                <LoginPage onLogin={handleLogin} />
              ) : (
                <Navigate to="/" replace />
              )
            }
          />
          <Route
            path="/"
            element={
              isAuthenticated ? (
                usuario?.rol === 'JEFE_CARRERA' ? (
                  <JefeCarreraDashboard usuario={usuario} />
                ) : usuario?.rol === 'SUPERUSUARIO' ? (
                  <SuperusuarioDashboard usuario={usuario} />
                ) : (
                  <Box sx={{ p: 4, textAlign: 'center' }}>
                    <Typography variant="h6">Rol no reconocido</Typography>
                  </Box>
                )
              ) : (
                <Navigate to="/login" replace />
              )
            }
          />
          <Route
            path="*"
            element={<Navigate to="/" replace />}
          />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

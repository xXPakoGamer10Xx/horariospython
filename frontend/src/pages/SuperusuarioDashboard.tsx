import React, { useState } from 'react';
import {
  Container,
  Typography,
  Button,
  Box,
  Grid,
  Card,
  CardContent,
  CardActions,
  Alert,
  List,
  ListItem,
  ListItemText,
  Fab
} from '@mui/material';
import { Add as AddIcon, PersonAdd as PersonAddIcon } from '@mui/icons-material';
import { adminService } from '../services/api';
import RegisterJefeCarreraDialog from '../components/RegisterJefeCarreraDialog';

interface SuperusuarioDashboardProps {
  usuario: any;
}

const SuperusuarioDashboard = ({ usuario }: SuperusuarioDashboardProps) => {
  const [registerDialogOpen, setRegisterDialogOpen] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  const handleRegisterSuccess = () => {
    setMessage('Jefe de Carrera registrado exitosamente');
    setRegisterDialogOpen(false);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Panel de Administración - Superusuario
        </Typography>
        
        {message && (
          <Alert severity="success" sx={{ mb: 2 }} onClose={() => setMessage('')}>
            {message}
          </Alert>
        )}
        
        {error && (
          <Alert severity="error" sx={{ mb: 2 }} onClose={() => setError('')}>
            {error}
          </Alert>
        )}

        <Grid container spacing={3}>
          {/* Gestión de Usuarios */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Gestión de Usuarios
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Administra los usuarios del sistema y asigna roles.
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="• Crear Jefes de Carrera" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Asignar carreras a usuarios" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Gestionar permisos" />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button
                  variant="contained"
                  startIcon={<PersonAddIcon />}
                  onClick={() => setRegisterDialogOpen(true)}
                  fullWidth
                >
                  Registrar Jefe de Carrera
                </Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Gestión de Carreras */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Gestión de Carreras
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Administra las carreras universitarias del sistema.
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="• Crear nuevas carreras" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Editar información de carreras" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Ver estadísticas por carrera" />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button variant="outlined" fullWidth>
                  Gestionar Carreras
                </Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Reportes del Sistema */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Reportes del Sistema
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Accede a reportes y estadísticas generales.
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="• Uso del sistema por carrera" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Horarios generados" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Actividad de usuarios" />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button variant="outlined" fullWidth>
                  Ver Reportes
                </Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Configuración Global */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Configuración Global
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Configura parámetros globales del sistema.
                </Typography>
                <List dense>
                  <ListItem>
                    <ListItemText primary="• Horarios de funcionamiento" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Restricciones generales" />
                  </ListItem>
                  <ListItem>
                    <ListItemText primary="• Parámetros de optimización" />
                  </ListItem>
                </List>
              </CardContent>
              <CardActions>
                <Button variant="outlined" fullWidth>
                  Configurar Sistema
                </Button>
              </CardActions>
            </Card>
          </Grid>
        </Grid>
      </Box>

      {/* Dialog para registrar Jefe de Carrera */}
      <RegisterJefeCarreraDialog
        open={registerDialogOpen}
        onClose={() => setRegisterDialogOpen(false)}
        onSuccess={handleRegisterSuccess}
      />
    </Container>
  );
};

export default SuperusuarioDashboard;

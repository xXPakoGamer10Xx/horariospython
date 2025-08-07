import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Button,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Alert,
  CircularProgress,
  Box
} from '@mui/material';
import { adminService } from '../services/api';
import { Carrera } from '../types';

interface RegisterJefeCarreraDialogProps {
  open: boolean;
  onClose: () => void;
  onSuccess: () => void;
}

interface RegisterForm {
  email: string;
  password: string;
  nombre_completo: string;
  id_carrera: number | '';
}

const RegisterJefeCarreraDialog = ({
  open,
  onClose,
  onSuccess
}: RegisterJefeCarreraDialogProps) => {
  const [form, setForm] = useState<RegisterForm>({
    email: '',
    password: '',
    nombre_completo: '',
    id_carrera: ''
  });
  const [carreras, setCarreras] = useState<Carrera[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (open) {
      loadCarreras();
    }
  }, [open]);

  const loadCarreras = async () => {
    try {
      const data = await adminService.getCarreras();
      setCarreras(data);
    } catch (err) {
      setError('Error al cargar carreras');
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value
    });
  };

  const handleCarreraChange = (e: any) => {
    setForm({
      ...form,
      id_carrera: e.target.value as number
    });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    if (!form.id_carrera) {
      setError('Debe seleccionar una carrera');
      setLoading(false);
      return;
    }

    try {
      const userData = {
        email: form.email,
        password: form.password,
        nombre_completo: form.nombre_completo,
        rol: 'JEFE_CARRERA' as const,
        id_carrera: form.id_carrera as number
      };

      await adminService.createUsuario(userData);
      onSuccess();
      onClose();
      setForm({
        email: '',
        password: '',
        nombre_completo: '',
        id_carrera: ''
      });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Error al registrar usuario');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setForm({
      email: '',
      password: '',
      nombre_completo: '',
      id_carrera: ''
    });
    setError('');
    onClose();
  };

  return (
    <Dialog open={open} onClose={handleClose} maxWidth="sm" fullWidth>
      <DialogTitle>Registrar Nuevo Jefe de Carrera</DialogTitle>
      <Box component="form" onSubmit={handleSubmit}>
        <DialogContent>
          {error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              {error}
            </Alert>
          )}

          <TextField
            fullWidth
            label="Nombre Completo"
            name="nombre_completo"
            value={form.nombre_completo}
            onChange={handleInputChange}
            margin="normal"
            required
            disabled={loading}
          />

          <TextField
            fullWidth
            label="Email"
            name="email"
            type="email"
            value={form.email}
            onChange={handleInputChange}
            margin="normal"
            required
            disabled={loading}
          />

          <TextField
            fullWidth
            label="Contraseña"
            name="password"
            type="password"
            value={form.password}
            onChange={handleInputChange}
            margin="normal"
            required
            disabled={loading}
          />

          <FormControl fullWidth margin="normal" required>
            <InputLabel>Carrera</InputLabel>
            <Select
              value={form.id_carrera}
              label="Carrera"
              onChange={handleCarreraChange}
              disabled={loading}
            >
              {carreras.map((carrera) => (
                <MenuItem key={carrera.id} value={carrera.id}>
                  {carrera.nombre}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </DialogContent>

        <DialogActions>
          <Button onClick={handleClose} disabled={loading}>
            Cancelar
          </Button>
          <Button
            type="submit"
            variant="contained"
            disabled={loading || !form.email || !form.password || !form.nombre_completo || !form.id_carrera}
          >
            {loading ? <CircularProgress size={24} /> : 'Registrar'}
          </Button>
        </DialogActions>
      </Box>
    </Dialog>
  );
};

export default RegisterJefeCarreraDialog;

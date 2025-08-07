import React, { useState, useEffect, useRef } from 'react';
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
  CircularProgress,
  Fab
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import { scheduleService } from '../services/api';
import { Profesor, ScheduleGenerationRequest } from '../types';
import ScheduleGrid from '../components/ScheduleGrid';

interface JefeCarreraDashboardProps {
  usuario: any; // Se puede definir tipo más específico
}

const JefeCarreraDashboard = ({ usuario }: JefeCarreraDashboardProps) => {
  const [profesores, setProfesores] = useState<Profesor[]>([]);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const profesoresFileRef = useRef<HTMLInputElement | null>(null);
  const materiasFileRef = useRef<HTMLInputElement | null>(null);

  useEffect(() => {
    loadProfesores();
    
    // Crear elementos input programáticamente para evitar problemas de JSX
    const profesoresInput = document.createElement('input');
    profesoresInput.type = 'file';
    profesoresInput.accept = '.xlsx,.xls';
    profesoresInput.style.display = 'none';
    profesoresInput.onchange = handleProfesorFileChange;
    profesoresFileRef.current = profesoresInput;
    document.body.appendChild(profesoresInput);

    const materiasInput = document.createElement('input');
    materiasInput.type = 'file';
    materiasInput.accept = '.xlsx,.xls';
    materiasInput.style.display = 'none';
    materiasInput.onchange = handleMateriaFileChange;
    materiasFileRef.current = materiasInput;
    document.body.appendChild(materiasInput);

    return () => {
      // Cleanup
      if (profesoresFileRef.current && document.body.contains(profesoresFileRef.current)) {
        document.body.removeChild(profesoresFileRef.current);
      }
      if (materiasFileRef.current && document.body.contains(materiasFileRef.current)) {
        document.body.removeChild(materiasFileRef.current);
      }
    };
  }, []);

  const loadProfesores = async () => {
    if (!usuario.id_carrera) return;
    
    setLoading(true);
    try {
      const data = await scheduleService.getProfesoresByCarrera(usuario.id_carrera);
      setProfesores(data);
    } catch (err: any) {
      setError('Error al cargar profesores');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateSchedule = async () => {
    if (!usuario.id_carrera) return;
    
    setGenerating(true);
    setError('');
    setMessage('');
    
    try {
      const request: ScheduleGenerationRequest = {
        id_carrera: usuario.id_carrera
      };
      
      const response = await scheduleService.generateSchedule(request);
      
      if (response.success) {
        setMessage(`Horarios generados exitosamente para ${response.generated_schedules.length} grupos`);
      } else {
        setError(response.message);
      }
    } catch (err: any) {
      setError('Error al generar horarios');
    } finally {
      setGenerating(false);
    }
  };

  const handleFileUpload = async (file: File, type: 'profesores' | 'materias') => {
    if (!usuario.id_carrera) return;
    
    setLoading(true);
    try {
      let result;
      if (type === 'profesores') {
        result = await scheduleService.importProfesores(usuario.id_carrera, file);
      } else {
        result = await scheduleService.importMaterias(usuario.id_carrera, file);
      }
      
      if (result.success) {
        setMessage(`${result.message}. ${result.errors.length > 0 ? `Errores: ${result.errors.length}` : ''}`);
        if (type === 'profesores') {
          loadProfesores();
        }
      } else {
        setError(result.message);
      }
    } catch (err: any) {
      setError(`Error al importar ${type}`);
    } finally {
      setLoading(false);
    }
  };

  const handleProfesorFileSelect = () => {
    if (profesoresFileRef.current) {
      profesoresFileRef.current.click();
    }
  };

  const handleMateriaFileSelect = () => {
    if (materiasFileRef.current) {
      materiasFileRef.current.click();
    }
  };

  const handleProfesorFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];
    if (file) handleFileUpload(file, 'profesores');
  };

  const handleMateriaFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const file = target.files?.[0];
    if (file) handleFileUpload(file, 'materias');
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Panel de {usuario.carrera?.nombre || 'Jefe de Carrera'}
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
          {/* Sección de importación */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Importar Datos
                </Typography>
                <Box sx={{ mb: 2 }}>
                  <Button
                    variant="outlined"
                    fullWidth
                    sx={{ mb: 1 }}
                    onClick={handleProfesorFileSelect}
                  >
                    Importar Profesores (.xlsx)
                  </Button>
                </Box>
                <Box>
                  <Button
                    variant="outlined"
                    fullWidth
                    onClick={handleMateriaFileSelect}
                  >
                    Importar Materias (.xlsx)
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>

          {/* Sección de generación */}
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Generar Horarios
                </Typography>
                <Typography variant="body2" color="textSecondary" paragraph>
                  Genera automáticamente los horarios para todos los grupos de la carrera.
                  Se crearán 2 versiones de horario por cada grupo.
                </Typography>
              </CardContent>
              <CardActions>
                <Button
                  variant="contained"
                  color="primary"
                  onClick={handleGenerateSchedule}
                  disabled={generating || profesores.length === 0}
                  fullWidth
                >
                  {generating ? <CircularProgress size={24} /> : 'Generar Horarios'}
                </Button>
              </CardActions>
            </Card>
          </Grid>

          {/* Lista de profesores */}
          <Grid item xs={12}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  Profesores de la Carrera ({profesores.length})
                </Typography>
                {loading ? (
                  <CircularProgress />
                ) : (
                  <Grid container spacing={2}>
                    {profesores.map((profesor) => (
                      <Grid item xs={12} sm={6} md={4} key={profesor.id}>
                        <Card variant="outlined">
                          <CardContent>
                            <Typography variant="subtitle2">
                              {profesor.nombre_completo}
                            </Typography>
                            <Typography variant="caption" display="block">
                              {profesor.numero_empleado} - {profesor.tipo_profesor}
                            </Typography>
                          </CardContent>
                        </Card>
                      </Grid>
                    ))}
                  </Grid>
                )}
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default JefeCarreraDashboard;

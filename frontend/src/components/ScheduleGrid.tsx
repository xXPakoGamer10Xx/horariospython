import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Typography,
  Box
} from '@mui/material';
import { HorarioGenerado } from '../types';

interface ScheduleGridProps {
  horarios: HorarioGenerado[];
  title?: string;
}

const dias = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado'];
const horas = ['07:00', '08:00', '09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'];

const ScheduleGrid = ({ horarios, title = "Horario" }: ScheduleGridProps) => {
  // Crear matriz de horarios para fácil renderizado
  const createScheduleMatrix = () => {
    const matrix: { [key: string]: HorarioGenerado | null } = {};
    
    horas.forEach(hora => {
      dias.forEach(dia => {
        const key = `${dia}-${hora}`;
        const horario = horarios.find(h => 
          h.dia_semana === dia && h.hora_inicio === hora + ':00'
        );
        matrix[key] = horario || null;
      });
    });
    
    return matrix;
  };

  const scheduleMatrix = createScheduleMatrix();

  const getCellContent = (dia: string, hora: string) => {
    const key = `${dia}-${hora}`;
    const horario = scheduleMatrix[key];
    
    if (!horario) return null;
    
    return (
      <Box sx={{ p: 1, textAlign: 'center' }}>
        <Typography variant="body2" fontWeight="bold">
          {horario.materia.nombre_materia}
        </Typography>
        <Typography variant="caption" display="block">
          {horario.profesor.nombre_completo}
        </Typography>
      </Box>
    );
  };

  return (
    <Box sx={{ mb: 4 }}>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <TableContainer component={Paper}>
        <Table size="small">
          <TableHead>
            <TableRow>
              <TableCell>Hora</TableCell>
              {dias.map(dia => (
                <TableCell key={dia} align="center">
                  {dia}
                </TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {horas.map(hora => (
              <TableRow key={hora}>
                <TableCell component="th" scope="row">
                  {hora}
                </TableCell>
                {dias.map(dia => (
                  <TableCell key={`${dia}-${hora}`} align="center" sx={{ minWidth: 150, height: 80 }}>
                    {getCellContent(dia, hora)}
                  </TableCell>
                ))}
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default ScheduleGrid;

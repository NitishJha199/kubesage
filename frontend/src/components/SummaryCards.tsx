import {
  Grid,
  Paper,
  Typography,
  Stack,
} from "@mui/material";

import ErrorIcon from "@mui/icons-material/Error";
import WarningAmberIcon from "@mui/icons-material/WarningAmber";
import CheckCircleIcon from "@mui/icons-material/CheckCircle";
import StorageIcon from "@mui/icons-material/Storage";

import type { Diagnosis } from "../types/diagnosis";

interface Props {
  diagnosis: Diagnosis[];
}

export default function SummaryCards({ diagnosis }: Props) {
  const critical = diagnosis.filter(
    (d) => d.severity === "CRITICAL"
  ).length;

  const warning = diagnosis.filter(
    (d) => d.severity === "WARNING"
  ).length;

  const healthy = diagnosis.filter(
    (d) => d.severity === "INFO"
  ).length;

  const cards = [
    {
      title: "Critical",
      value: critical,
      icon: <ErrorIcon fontSize="large" />,
      color: "#d32f2f",
    },
    {
      title: "Warning",
      value: warning,
      icon: <WarningAmberIcon fontSize="large" />,
      color: "#ed6c02",
    },
    {
      title: "Healthy",
      value: healthy,
      icon: <CheckCircleIcon fontSize="large" />,
      color: "#2e7d32",
    },
    {
      title: "Resources",
      value: diagnosis.length,
      icon: <StorageIcon fontSize="large" />,
      color: "#1565c0",
    },
  ];

  return (
    <Grid container spacing={3} sx={{ mb: 5 }}>
      {cards.map((card) => (
        <Grid key={card.title} size={{ xs: 12, sm: 6, md: 3 }}>
          <Paper
            elevation={3}
            sx={{
              p: 3,
              borderRadius: 3,
              transition: "0.2s",
              "&:hover": {
                transform: "translateY(-4px)",
              },
            }}
          >
            <Stack
              direction="row"
              justifyContent="space-between"
              alignItems="center"
            >
              <div>
                <Typography
                  color="text.secondary"
                  variant="body2"
                >
                  {card.title}
                </Typography>

                <Typography
                  variant="h3"
                  fontWeight="bold"
                >
                  {card.value}
                </Typography>
              </div>

              <div
                style={{
                  color: card.color,
                }}
              >
                {card.icon}
              </div>
            </Stack>
          </Paper>
        </Grid>
      ))}
    </Grid>
  );
}

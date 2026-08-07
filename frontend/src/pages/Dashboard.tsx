import { useEffect, useMemo, useState } from "react";

import {
  Alert,
  Button,
  Chip,
  CircularProgress,
  Container,
  Stack,
  TextField,
  Typography,
} from "@mui/material";

import { getDiagnosis } from "../api/kubesage";
import type { Diagnosis } from "../types/diagnosis";

import SummaryCards from "../components/SummaryCards";
import DiagnosisGrid from "../components/DiagnosisGrid";

export default function Dashboard() {
  const [diagnosis, setDiagnosis] = useState<Diagnosis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [search, setSearch] = useState("");
  const [filter, setFilter] = useState("All");

  async function loadDiagnosis() {
    setLoading(true);

    try {
      const data = await getDiagnosis();
      setDiagnosis(data);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Unable to connect to KubeSage API.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDiagnosis();
  }, []);

  const filteredDiagnosis = useMemo(() => {
    return diagnosis.filter((item) => {
      const matchesSearch = `
        ${item.resource_name}
        ${item.resource_type}
        ${item.namespace}
        ${item.diagnosis}
      `
        .toLowerCase()
        .includes(search.toLowerCase());

      const matchesFilter =
        filter === "All" || item.resource_type === filter;

      return matchesSearch && matchesFilter;
    });
  }, [diagnosis, search, filter]);

  const filters = [
    "All",
    "Pod",
    "Deployment",
    "Service",
    "PersistentVolumeClaim",
    "PersistentVolume",
    "Node",
  ];

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 5 }}>
      {loading && <CircularProgress />}

      {error && <Alert severity="error">{error}</Alert>}

      {!loading && !error && (
        <>
          <SummaryCards diagnosis={filteredDiagnosis} />

          <Stack
            direction="row"
            justifyContent="space-between"
            alignItems="center"
            sx={{ mb: 3 }}
          >
            <Typography variant="h5" fontWeight="bold">
              Diagnosis Results
            </Typography>

            <Button
              variant="contained"
              onClick={loadDiagnosis}
            >
              Refresh
            </Button>
          </Stack>

          <TextField
            fullWidth
            placeholder="🔍 Search resources..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            sx={{ mb: 3 }}
          />

          <Stack
            direction="row"
            spacing={1}
            flexWrap="wrap"
            useFlexGap
            sx={{ mb: 4 }}
          >
            {filters.map((item) => (
              <Chip
                key={item}
                label={item}
                clickable
                color={filter === item ? "primary" : "default"}
                onClick={() => setFilter(item)}
              />
            ))}
          </Stack>

          <DiagnosisGrid diagnosis={filteredDiagnosis} />
        </>
      )}
    </Container>
  );
}

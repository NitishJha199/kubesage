import Grid from "@mui/material/Grid";
import type { Diagnosis } from "../types/diagnosis";
import DiagnosisCard from "./DiagnosisCard";

interface Props {
  diagnosis: Diagnosis[];
}

export default function DiagnosisGrid({ diagnosis }: Props) {
  return (
    <Grid container spacing={3}>
      {diagnosis.map((item) => (
        <Grid
          key={`${item.resource_type}-${item.resource_name}`}
          size={{ xs: 12, md: 6 }}
        >
          <DiagnosisCard diagnosis={item} />
        </Grid>
      ))}
    </Grid>
  );
}

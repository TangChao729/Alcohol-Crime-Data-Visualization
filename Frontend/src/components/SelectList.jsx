import * as React from 'react';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

export default function SelectList(props) {
  const [year, setYear] = React.useState("");
  const handleChange = (event) => {
    setYear(event.target.value);
    props.onYearChange(event.target.value);
  };

  return (
    <FormControl sx={{ m: 1, minWidth: 120 }} size="small">
      <InputLabel id="demo-select-small-label">Year</InputLabel>
      <Select
        labelId="demo-select-small-label"
        id="demo-select-small"
        value={year}
        label="Year"
        onChange={handleChange}
      >
        <MenuItem value="">
        </MenuItem>
        <MenuItem value={"2017"}>2017</MenuItem>
        <MenuItem value={"2018"}>2018</MenuItem>
        <MenuItem value={"2019"}>2019</MenuItem>
      </Select>
    </FormControl>
  );
}
import * as React from "react";
import TextField from "@mui/material/TextField";

const Cell = ({ cell, handleOnChange, id, solve, answer }) => {
  const { bottom, left, right, top, value } = cell;

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        width: "85px",
        height: "85px",
        borderTop: !top ? "solid 2px black" : "solid 2px rgb(200,200,200)",
        borderBottom: !bottom
          ? "solid 2px black"
          : "solid 2px rgb(200,200,200)",
        borderRight: !right ? "solid 2px black" : "solid 2px rgb(200,200,200)",
        borderLeft: !left ? "solid 2px black" : "solid 2px rgb(200,200,200)",
      }}
    >
      <span
        style={{ paddingTop: "4px", marginLeft: "5px", alignSelf: "start" }}
      >
        {value != 0 ? value : ""}
      </span>
      <TextField
        style={{
          width: 70,
          marginBottom: "15px",
          paddingTop: value == 0 ? "22px" : "0px",
        }}
        id="outlined-basic"
        variant="outlined"
        type="number"
        value={solve ? answer : null}
        disabled={solve}
        onChange={(e) => handleOnChange(e.target.value, id)}
      />
    </div>
  );
};

export default Cell;

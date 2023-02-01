CREATE TABLE TF_Glyco (
    cell_type_id	varchar(100) NOT NULL,
    TF	varchar(100) NOT NULL,
    Target	varchar(100) NOT NULL,
    confidence	real NOT NULL
);

CREATE INDEX cell_type_idx ON TF_Glyco (cell_type_id);
CREATE INDEX confidence_idx ON TF_Glyco (confidence);
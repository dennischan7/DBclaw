# Oracle 23c - graph_table-operator
Source: https://docs.oracle.com/en/database/oracle/oracle-database/23/sqlrf/graph_table-operator.html

Setting Up Sample Data

This example creates a property graph, `students_graph`, using `persons`,`university`, `friendships`, and `students` as the underlying database tables for the graph.

The following statements first create the necessary tables and fill them with sample data:

```
CREATE TABLE university (
    id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    name VARCHAR2(10),
    CONSTRAINT u_pk PRIMARY KEY (id));
INSERT INTO university (name) VALUES ('ABC');
INSERT INTO university (name) VALUES ('XYZ');
```

```
CREATE TABLE persons (
     person_id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT
     BY 1),
     name VARCHAR2(10),
     birthdate DATE,
     height FLOAT DEFAULT ON NULL 0,
     person_data JSON,
     CONSTRAINT person_pk PRIMARY KEY (person_id));

INSERT INTO persons (name, height, birthdate, person_data)
       VALUES ('John', 1.80, to_date('13/06/1963', 'DD/MM/YYYY'), '{"department":"IT","role":"Software Developer"}');

INSERT INTO persons (name, height, birthdate, person_data)
       VALUES ('Mary', 1.65, to_date('25/09/1982', 'DD/MM/YYYY'), '{"department":"HR","role":"HR Manager"}');

INSERT INTO persons (name, height, birthdate, person_data)
       VALUES ('Bob', 1.75, to_date('11/03/1966', 'DD/MM/YYYY'), '{"department":"IT","role":"Technical Consultant"}');

INSERT INTO persons (name, height, birthdate, person_data)
       VALUES ('Alice', 1.70, to_date('01/02/1987', 'DD/MM/YYYY'), '{"department":"HR","role":"HR Assistant"}');
```

```
CREATE TABLE students (
      s_id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
      s_univ_id NUMBER,
      s_person_id NUMBER,
      subject VARCHAR2(10),      
      CONSTRAINT stud_pk PRIMARY KEY (s_id),
      CONSTRAINT stud_fk_person FOREIGN KEY (s_person_id) REFERENCES persons(person_id),
      CONSTRAINT stud_fk_univ FOREIGN KEY (s_univ_id) REFERENCES university(id)
    );

INSERT INTO students(s_univ_id, s_person_id,subject) VALUES (1,1,'Arts');
INSERT INTO students(s_univ_id, s_person_id,subject) VALUES (1,3,'Music');
INSERT INTO students(s_univ_id, s_person_id,subject) VALUES (2,2,'Math');
INSERT INTO students(s_univ_id, s_person_id,subject) VALUES (2,4,'Science');
```

```
CREATE TABLE friendships (
    friendship_id NUMBER GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1),
    person_a NUMBER,
    person_b NUMBER,
    meeting_date DATE,
    CONSTRAINT fk_person_a_id FOREIGN KEY (person_a) REFERENCES persons(person_id),
    CONSTRAINT fk_person_b_id FOREIGN KEY (person_b) REFERENCES persons(person_id),
    CONSTRAINT fs_pk PRIMARY KEY (friendship_id)
);

INSERT INTO friendships (person_a, person_b, meeting_date) VALUES (1, 3, to_date('01/09/2000', 'DD/MM/YYYY'));
INSERT INTO friendships (person_a, person_b, meeting_date) VALUES (2, 4, to_date('19/09/2000', 'DD/MM/YYYY'));
INSERT INTO friendships (person_a, person_b, meeting_date) VALUES (2, 1, to_date('19/09/2000', 'DD/MM/YYYY'));
INSERT INTO friendships (person_a, person_b, meeting_date) VALUES (3, 2, to_date('10/07/2001', 'DD/MM/YYYY'));
```

The following statement creates a graph on top of the tables:

```
CREATE PROPERTY GRAPH students_graph
  VERTEX TABLES (
    persons KEY (person_id)
      LABEL person
        PROPERTIES (person_id, name, birthdate AS dob)
      LABEL person_ht
        PROPERTIES (height),
    university KEY (id)
  )
  EDGE TABLES (
    friendships AS friends
      KEY (friendship_id)
      SOURCE KEY (person_a) REFERENCES persons(person_id)
      DESTINATION KEY (person_b) REFERENCES persons(person_id)
      PROPERTIES (friendship_id, meeting_date),
    students AS student_of
      SOURCE KEY (s_person_id) REFERENCES persons(person_id)
      DESTINATION KEY (s_univ_id) REFERENCES university(id)
      PROPERTIES (subject)
  );
```

This creates the following graph:
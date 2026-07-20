ThisBuild / version      := "1.0.0"
ThisBuild / scalaVersion := "2.13.12"
ThisBuild / organization := "edu.universidad"

lazy val root = (project in file("."))
  .settings(
    name := "seleccion-personal",

    libraryDependencies ++= Seq(
      "io.circe" %% "circe-core"    % "0.14.6",
      "io.circe" %% "circe-generic" % "0.14.6",
      "io.circe" %% "circe-parser"  % "0.14.6"
    ),

    scalacOptions ++= Seq(
      "-deprecation",
      "-feature",
      "-unchecked",
      "-encoding", "utf8"
    )
  )

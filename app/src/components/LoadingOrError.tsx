import type { ReactElement } from "react";

interface Properties {
  error?: Error;
}
export default function LoadingOrError({ error }: Properties): ReactElement {
  return (
    <div className="min-h-screen flex items-center justify-center">
      <h1 className="text-xl">{error ? error.message : "Loading..."}</h1>
    </div>
  );
}

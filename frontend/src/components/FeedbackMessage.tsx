type FeedbackMessageProps = {
  type: "success" | "error" | "info";
  message: string;
};

export function FeedbackMessage({ type, message }: FeedbackMessageProps) {
  return (
    <div className={`feedback feedback-${type}`} role={type === "error" ? "alert" : "status"}>
      {message}
    </div>
  );
}

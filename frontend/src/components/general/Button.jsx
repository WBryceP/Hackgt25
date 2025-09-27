const Button = ({ children }) => {
  return (
    <button className="p-2 bg-primaryInvert text-primary rounded-md">
      {children}
    </button>
  );
};

export default Button;

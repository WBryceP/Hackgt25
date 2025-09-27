import Header from "./components/general/Header";
const Layout = ({ children }) => {
  return (
    <div className="bg-body text-primaryInvert min-h-screen text-xs sm:text-sm md:text-base">
      <Header />
      <div className="p-4">{children}</div>
      <div className="">Footer</div>
    </div>
  );
};

export default Layout;

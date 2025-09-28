const Loader = () => {
  return (
    <div className="flex justify-center items-center flex-col gap-2 text-xl">
      <span className="w-12 h-12 border-[5px] border-dotted border-primaryInvert rounded-full inline-block animate-[spin_3s_linear_infinite]"></span>
      <p>Estimated time: 2 minutes</p>
    </div>
  );
};

export default Loader;

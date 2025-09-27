const Sources = ({ sources, setSources }) => {
  return (
    <div>
      <ul className="mb-2 text-sm flex flex-col gap-2">
        {sources.map((source, index) => {
          return (
            <li key={source.sourceName + index} className="">
              {source.sourceName}
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default Sources;

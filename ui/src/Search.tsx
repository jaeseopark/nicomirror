import { useState, useEffect, useRef, forwardRef, useMemo } from "react";
import {
  Input,
  InputGroup,
  InputLeftElement,
  Popover,
  PopoverTrigger,
  PopoverContent,
  PopoverBody,
  PopoverArrow,
  useDisclosure,
} from "@chakra-ui/react";
import { Search2Icon } from "@chakra-ui/icons";

import { useNav } from "./hooks/useNav";
import { Classification, classifySearchTerm } from "./utils/regex";

const SearchInputGroup = forwardRef(({ input, onChange }: { input: string; onChange: (newInput: string) => void }, ref: any) => (
  <InputGroup borderRadius={5} size="sm">
    <InputLeftElement pointerEvents="none" children={<Search2Icon color="gray.600" />} />
    <Input
      ref={ref}
      type="text"
      placeholder="Search..."
      border="1px solid #949494"
      value={input}
      onChange={(e) => onChange(e?.target?.value || "")}
    />
  </InputGroup>
));

const SearchResultsView = ({ input }: { input: string }): JSX.Element => {
  const classification: Classification = useMemo(() => classifySearchTerm(input), [input]);
  const { navVideo, navPlaylist } = useNav();

  if (classification.type === "video") {
    return (
      <div>
        <label onClick={() => navVideo(classification.sanitized)}>{classification.sanitized}</label>
      </div>
    );
  }

  if (classification.type === "playlist") {
    return (
      <div>
        <label onClick={() => navPlaylist(classification.sanitized)}>{classification.sanitized}</label>
      </div>
    );
  }

  return <div>TODO: implement other things</div>;
};

export const Search = () => {
  const [userInput, setuserInput] = useState("");
  const { isOpen, onToggle, onClose } = useDisclosure();
  const focusRef = useRef(null);

  useEffect(() => {
    if (userInput && !isOpen) {
      onToggle();
    }
  }, [userInput]);

  return (
    <Popover initialFocusRef={focusRef} isOpen={isOpen} onClose={onClose} placement="bottom" closeOnBlur={true}>
      <PopoverTrigger>
        <SearchInputGroup input={userInput} onChange={setuserInput} />
      </PopoverTrigger>
      <PopoverContent color="white" bg="blue.800" borderColor="blue.800">
        <PopoverArrow bg="blue.800" />
        <PopoverBody>
          <SearchInputGroup ref={focusRef} input={userInput} onChange={setuserInput} />
          <SearchResultsView input={userInput} />
        </PopoverBody>
      </PopoverContent>
    </Popover>
  );
};

export default Search;

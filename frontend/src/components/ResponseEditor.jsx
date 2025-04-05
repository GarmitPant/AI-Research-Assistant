import React, { useEffect } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';

const ResponseEditor = ({ content, onChange }) => {
  useEffect(() => {
    // Initialize the editor with content when it changes from parent
    if (content && !document.querySelector('.ql-editor').innerHTML.trim()) {
      onChange(content);
    }
  }, [content]);

  const modules = {
    toolbar: [
      [{ 'header': [1, 2, 3, false] }],
      ['bold', 'italic', 'underline', 'strike'],
      [{ 'list': 'ordered'}, { 'list': 'bullet' }],
      [{ 'indent': '-1'}, { 'indent': '+1' }],
      ['link'],
      ['clean']
    ],
  };

  const formats = [
    'header',
    'bold', 'italic', 'underline', 'strike',
    'list', 'bullet', 'indent',
    'link'
  ];

  return (
    <div className="response-editor">
      <ReactQuill 
        theme="snow"
        value={content}
        onChange={onChange}
        modules={modules}
        formats={formats}
        placeholder="Your response will appear here. You can edit it as needed."
        className="h-64"
      />
      <div className="mt-4 flex justify-end">
        <button
          onClick={() => {
            navigator.clipboard.writeText(content.replace(/<[^>]*>/g, ' '));
          }}
          className="px-4 py-2 bg-gray-200 hover:bg-gray-300 rounded-md text-gray-700 font-medium"
        >
          Copy to Clipboard
        </button>
      </div>
    </div>
  );
};

export default ResponseEditor;

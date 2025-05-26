import { useState } from 'react';

interface ShiftData {
  date: string;
  startTime: string;
  endTime: string;
}

const ShiftForm = () => {
  const [shifts, setShifts] = useState<ShiftData[]>([]);
  const [currentShift, setCurrentShift] = useState<ShiftData>({
    date: '',
    startTime: '',
    endTime: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setCurrentShift((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (currentShift.date && currentShift.startTime && currentShift.endTime) {
      setShifts((prev) => [...prev, currentShift]);
      setCurrentShift({
        date: '',
        startTime: '',
        endTime: '',
      });
    }
  };

  return (
    <div className="max-w-md mx-auto p-6 bg-white rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold mb-6 text-gray-800">シフト提出フォーム</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label htmlFor="date" className="block text-sm font-medium text-gray-700">
            日付
          </label>
          <input
            type="date"
            id="date"
            name="date"
            value={currentShift.date}
            onChange={handleInputChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
        <div>
          <label htmlFor="startTime" className="block text-sm font-medium text-gray-700">
            開始時間
          </label>
          <input
            type="time"
            id="startTime"
            name="startTime"
            value={currentShift.startTime}
            onChange={handleInputChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
        <div>
          <label htmlFor="endTime" className="block text-sm font-medium text-gray-700">
            終了時間
          </label>
          <input
            type="time"
            id="endTime"
            name="endTime"
            value={currentShift.endTime}
            onChange={handleInputChange}
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
        >
          シフトを追加
        </button>
      </form>

      {shifts.length > 0 && (
        <div className="mt-8">
          <h3 className="text-lg font-semibold mb-4 text-gray-800">提出済みシフト</h3>
          <div className="space-y-2">
            {shifts.map((shift, index) => (
              <div
                key={index}
                className="p-3 bg-gray-50 rounded-md border border-gray-200"
              >
                <p className="text-sm text-gray-600">
                  日付: {shift.date}
                </p>
                <p className="text-sm text-gray-600">
                  時間: {shift.startTime} - {shift.endTime}
                </p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ShiftForm; 